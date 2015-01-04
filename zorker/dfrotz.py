import re
import pexpect


class DFrotz(object):
    def __init__(self, game_file, interpreter='dfrotz'):
        self.dfrotz = pexpect.spawn('%s %s' % (interpreter, game_file))
        self.re = re.compile('\n((?P<location>.*)Score\:\ '
                            '(?P<score>\d+)\s*Moves\:\ '
                            '(?P<moves>\d+))?\s*(?P<text>.+)\>',
                            re.DOTALL)

    def tell(self, line):
        self.dfrotz.sendline(line.strip())

    def listen(self):
        resp = self._response()
        raw = self.re.search(resp).groupdict()
        for k in ['score', 'location', 'moves']:
            if k in raw and raw[k]:
                setattr(self, k, raw[k].strip())
        return raw['text'].strip().replace('\n', ' ')

    def _response(self):
        res = []
        c = None
        while c != '>':
            try:
                c = self.dfrotz.read_nonblocking(1, 0.1)
                res.append(c)
            except Exception, msg:
                break
        return ''.join(res).replace('\r\n', '\n')
