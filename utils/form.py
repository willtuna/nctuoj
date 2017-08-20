import copy
from datetime import datetime
from enum import Enum

from dateutil import parser


class ERR_TYPE(Enum):
    REQUIRE = 1
    TYPE = 2
    NON_EMPTY = 3
    EXCEPT = 4
    RANGE = 5
    LEN_RANGE = 6


def custom_errmsg_format(err_type, item, exception=None):
    return None


def default_errmsg_format(err_type, item, exception=None):
    '''
    err_type: as above ERR_TYPE
    item: {
        ...options in schame,
        value,
    }
    exception: Exception threw when value can't be casted to right type
    '''
    err_msg = custom_errmsg_format(err_type, item, exception)
    desc = ''.join(x[0].upper() + x[1:] for x in item['desc'].split())
    if err_msg is not None:
        return err_msg
    if err_type == ERR_TYPE.REQUIRE:
        err_msg = '%s Is Not In Form.' % desc
    elif err_type == ERR_TYPE.TYPE:
        err_msg = '%s Must Be %s.' % (desc, item['type'].__name__)
    elif err_type == ERR_TYPE.NON_EMPTY:
        err_msg = '%s Can Not Be Empty.' % desc
    elif err_type == ERR_TYPE.EXCEPT:
        err_msg = '%s Can Not Be A Value Of %s.' % (item['value'], desc)
    elif err_type == ERR_TYPE.RANGE:
        err_msg = 'Value Of %s Must In Range[%s, %s].' % (desc, *item['range'])
    elif err_type == ERR_TYPE.LEN_RANGE:
        err_msg = 'Length Of Value Of %s Must In Range[%s, %s].' % (
            desc, *item['len_range'])
    return err_msg


def form_validation(form, schema):
    err = _form_validation(form, schema)
    return (400, err) if err else None


def register_custom_errmsg(custom):
    global custom_errmsg_format
    custom_errmsg_format = custom


def _form_validation(form, schema):
    '''
    schema:
        [{
            # require
            'name': <str> # +<str> means require, default is optional
            # optional
            'desc': <str>
            'type': <class>
            'each': <class>
            'non_empty': <bool> # for str, list
            'except': <list>
            'range': <tuple> # t[0] <= value <= t[1]
            'len_range': <tuple> # t[0] <= len(value) <= t[1]
            'check_dict': <dict> # for dict
            ...
        }]
    int
    str
    list
    set
    dict
    datetime
    '''
    key = list(form.keys())
    for item in key:
        exist = False
        for x in schema:
            if x['name'] == item or \
                    (x['name'][0] == '+' and x['name'][1:] == item):
                exist = True
        if not exist:
            del form[item]
            continue
        if form[item] is None:
            del form[item]
            continue

    for item in schema:
        require = True if item['name'][0] == '+' else False
        name = item['name'] = item['name'][1:] if require else item['name']
        item['desc'] = item.get('desc') or name

        # check require
        if require and (name not in form or form[name] is None):
            return default_errmsg_format(ERR_TYPE.REQUIRE, item)

        if not require and (name not in form or form[name] is None):
            continue

        item['value'] = form[name]

        # check value type
        if 'type' in item:
            if not isinstance(form[name], item['type']):
                if item['type'] == datetime:
                    try:
                        form[name] = item['value'] = parser.parse(form[name])
                    except Exception as e:
                        return default_errmsg_format(ERR_TYPE.TYPE, item, e)
                elif item['type'] == bool:
                    form[name] = True if form[name].lower(
                    ) in ['1', 'true', 'on'] else False
                else:
                    try:
                        form[name] = item['value'] = item['type'](form[name])
                    except Exception as e:
                        return default_errmsg_format(ERR_TYPE.TYPE, item, e)

        # check non_empty
        if 'non_empty' in item and item['non_empty']:
            if form[name] == item['type']() or form[name] is None:
                return default_errmsg_format(ERR_TYPE.NON_EMPTY, item)

        # check except
        if 'except' in item:
            if form[name] in item['except']:
                return default_errmsg_format(ERR_TYPE.EXCEPT, item)

        # check range
        if 'range' in item:
            if not (item['range'][0] <= form[name] <= item['range'][1]):
                return default_errmsg_format(ERR_TYPE.RANGE, item)

        # check len_range
        if 'len_range' in item:
            if not (
                    item['len_range'][0] <=
                    len(form[name]) <=
                    item['len_range'][1]
            ):
                return default_errmsg_format(ERR_TYPE.LEN_RANGE, item)

        # check check
        if 'check' in item:
            if isinstance(form[name], dict):
                err = _form_validation(form[name],
                                       copy.deepcopy(item['check']))
                if err:
                    return err
            elif isinstance(form[name], list):
                item['check']['name'] = '+%s' % name
                for i, ele in enumerate(form[name]):
                    data = {name: ele}
                    err = _form_validation(data,
                                           copy.deepcopy([item['check']]))
                    form[name][i] = data[name]
                    if err:
                        return err

    return None
