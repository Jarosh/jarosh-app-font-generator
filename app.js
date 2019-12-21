const exec = require('child_process').exec;
const fs = require('fs');
const MD5 = require('md5');
const express = require('express');
const cors = require('cors');
const router = express.Router();

const app = express();
const path = __dirname + '/tmp/';
const port = 8080;

// http://localhost:8080/v1/ascii;name:UnicodeBP/תיב־ףלארבע

function zerofill(str, len, right) {
    const fill = (str.length < len)
        ? new Array(len - str.length + 1).join('0')
        : '';
    return right
        ? str + fill
        : fill + str;
}

router.use(function (req, res, next) {
    console.log('/' + req.method);
    next();
});

router.get('/', function (req, res) {
    res.sendFile(`${__dirname}/app.html`);
});

router.get('/:ver/:opt/:str', function (req, res) {
    const opt = req.params.opt.toString('utf8').split(';').reduce((obj, str) => {
        const tmp = str.split(':');
        if (tmp.length <= 2) {
            obj[tmp[0]] = (tmp.length === 2) ? tmp[1] : true;
        } else {
            obj[tmp[0]] = [];
            for (let i = 1; i < tmp.length; i++) {
                obj[tmp[0]].push(tmp[i]);
            }
        }
        return obj;
    }, {});
    const cmd = 'bin/produce.py';
    const str = req.params.str.toString('utf8');
    const arr = [...(opt.ascii ? Array(0xFF + 1).keys() : [])];

    if (!opt.name || Array.isArray(opt.name)) {
        opt.name = 'JaroshUnicode';
    }

    for (let i = 0; i < [...str].length; i++) {
        const c = str.codePointAt(i);
        if (!arr.includes(c)) {
            arr.push(c);
        }
    }

    const arg = arr
        .sort((a, b) => (a - b))
        .map((i) => {
            const char = zerofill(i.toString(16).toUpperCase(), 4);
            const file = `u${char}-${char}.svg`;
            return fs.existsSync(`fonts/noto-sans-regular/${file}`) && `fonts/noto-sans-regular/${file}`
                || fs.existsSync(`fonts/unifont-12.1.03/${file}`) && `fonts/unifont-12.1.03/${file}`
                || null;
        })
        .filter((i) => {
            return !!i;
        });
    const md5 = MD5(arr.join(',') + '__' + opt.name);
    const ttf = `${__dirname}/tmp/${md5}.ttf`;

    try {
        if (fs.existsSync(ttf)) {
            res.download(ttf, `${md5}.ttf`);
        } else {
            exec(
                `${cmd} -o ${ttf} -n ${opt.name} ${arg.join(' ')}`,
                function(error, stdout, stderr) {
                    if (!error) {
                        res.download(ttf, `${md5}.ttf`);
                    } else {
                        res.send(error);
                    }
                }
            );
        }
    } catch(err) {
        res.send(err);
    }
});

app.use(cors());
app.use('/', router);

app.listen(port, function () {
    console.log(`App is listening on port ${port}`)
});
