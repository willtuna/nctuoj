import json

from data_collector.base import Base


class Missions(Base):

    def post(self, req):
        args = ['mission', 'mission_list']
        data = req.get_args(args)
        try:
            data['mission_list'] = json.loads(data['mission_list'])
            if not isinstance(data['mission_list'], list):
                data['mission_list'] = []
        except:
            data['mission_list'] = []
        try:
            data['mission_list'].append(json.loads(data['mission']))
        except:
            pass

        for mission in data['mission_list']:
            if 'tick' not in mission:
                mission['tick'] = False
            if 'return' in mission:
                if 'payload' not in mission['return']:
                    mission['return']['payload'] = {}
            if 'prepare' not in mission:
                mission['prepare'] = {}
            if 'tasks' not in mission:
                mission['tasks'] = {}
            if 'final' not in mission:
                mission['final'] = {}
            for t in ['prepare', 'tasks', 'final']:
                if t == 'tasks':
                    if 'task' not in mission['tasks']:
                        mission['tasks']['task'] = []
                    for id, x in enumerate(mission['tasks']['task']):
                        if 'file' not in x:
                            x['file'] = {}
                        if 'macro' not in x:
                            x['macro'] = {}
                        x['macro']['__TASK_ID__'] = id
                else:
                    if 'file' not in mission[t]:
                        mission[t]['file'] = {}
                if 'execute' not in mission[t]:
                    mission[t]['execute'] = []
                for execute in mission[t]['execute']:
                    if 'name' not in execute:
                        execute['name'] = ''
                    if 'memory_limit' not in execute:
                        execute['memory_limit'] = 65536
                    if 'time_limit' not in execute:
                        execute['time_limit'] = 60000
                    if 'output_limit' not in execute:
                        execute['output_limit'] = 262144
                    if 'meta' not in execute:
                        execute['meta'] = 'meta'
                    if 'stdin' not in execute:
                        execute['stdin'] = ''
                    if 'stdout' not in execute:
                        execute['stdout'] = ''
                    if 'stderr' not in execute:
                        execute['stderr'] = ''
                    if 'record' not in execute:
                        execute['record'] = {}
                    if 'stdout' not in execute['record']:
                        execute['record']['stdout'] = 1024
                    if 'stderr' not in execute['record']:
                        execute['record']['stderr'] = 1024
                    if 'enable' not in execute['record']:
                        execute['record']['enable'] = True
                    if 'scope' not in execute:
                        execute['scope'] = {}
                    if 'import' not in execute['scope']:
                        execute['scope']['import'] = []
                    if 'export' not in execute['scope']:
                        execute['scope']['export'] = []
                    if 'enable' not in execute['scope']:
                        execute['scope']['enable'] = False
        return data
