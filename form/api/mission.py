import json

from form.base import Base


class Missions(Base):

    def execute_checker(self, data):
        required_args = [{
            'name': '+execute',
            'type': list,
            'check': {
                'type': dict,
                'check': [{
                    'name': '+name',
                    'type': str,
                }, {
                    'name': '+command',
                    'type': list,
                    'check': {
                        'type': str,
                    }
                }, {
                    'name': '+memory_limit',
                    'type': int,
                    'range': (0, 1 << 23),  # 8GB
                }, {
                    'name': '+time_limit',
                    'type': int,
                    'range': (1, 60000),  # 60 s
                }, {
                    'name': '+output_limit',
                    'type': int,
                    'range': (1, 262144),  # 256 MB
                }, {
                    'name': '+meta',
                    'type': str,
                    'len_range': (1, 256)
                }, {
                    'name': '+stdin',
                    'type': str,
                }, {
                    'name': '+stdout',
                    'type': str,
                }, {
                    'name': '+stderr',
                    'type': str,
                }, {
                    'name': '+record',
                    'type': dict,
                    'check': [{
                        'name': '+stdout',
                        'type': int,
                        'range': (0, 8388608),  # 128kb
                    }, {
                        'name': '+stderr',
                        'type': int,
                        'range': (0, 8388608),  # 128kb
                    }, {
                        'name': '+enable',
                        'type': bool,
                    }]
                }, {
                    'name': '+scope',
                    'type': dict,
                    'check': [{
                        'name': '+import',
                        'type': list,
                        'check': {
                            'type': str,
                        }
                    }, {
                        'name': '+export',
                        'type': list,
                        'check': {
                            'type': str,
                        }
                    }, {
                        'name': '+enable',
                        'type': bool
                    }]
                }]
            }
        }]
        return self.form_validation(data, required_args)

    def post(self, data):
        required_args = [{
            'name': '+mission_list',
            'type': list,
            'check': {
                'type': dict,
                'check': [{
                    'name': '+tick',
                    'type': bool,
                }, {
                    'name': '+return',
                    'type': dict,
                    'check': [{
                        'name': '+url',
                        'type': str,
                    }, {
                        'name': '+payload',
                        'type': dict,
                    }]
                }, {
                    'name': '+prepare',
                    'type': dict,
                    'check': [{
                        'name': '+file',
                        'type': dict,
                    }, {
                        'name': '+execute',
                        'type': list,
                    }]
                }, {
                    'name': '+tasks',
                    'type': dict,
                    'check': [{
                        'name': '+task',
                        'type': list,
                        'check': {
                            'type': dict,
                            'check': [{
                                'name': '+file',
                                'type': dict,
                            }, {
                                'name': '+macro',
                                'type': dict,
                            }]
                        }
                    }, {
                        'name': '+execute',
                        'type': list,
                    }]
                }, {
                    'name': '+final',
                    'type': dict,
                    'check': [{
                        'name': '+file',
                        'type': dict,
                    }, {
                        'name': '+execute',
                        'type': list,
                    }]
                }]
            }
        }, ]
        err = self.form_validation(data, required_args)
        if err:
            return err

        for mission in data['mission_list']:
            for t in ['prepare', 'final']:
                err = self.execute_checker({
                    'execute': mission[t]['execute']
                })
                if err:
                    return err
            for task in mission['tasks']['task']:
                task_execute = mission['tasks']['execute'].copy()
                task_execute = json.dumps(task_execute)
                for macro, value in task['macro'].items():
                    task_execute = task_execute.replace(macro, str(value))
                task_execute = json.loads(task_execute)
                err = self.execute_checker({
                    'execute': task_execute
                })
                if err:
                    return err
