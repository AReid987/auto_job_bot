import PinoPretty, { PrettyOptions } from 'pino-pretty';

import { DateTime } from 'luxon';
import { Params } from 'nestjs-pino';
import ansis from 'ansis';
import { randomUUID } from 'crypto';
import { startTime } from 'pino-http';

const logSymTheme = {
  trace: ansis.bold.gray,
  debug: ansis.bold.cyan,
  info: ansis.bold.fg(40),
  success: ansis.bold.fg(21),
  warn: ansis.bold.fg(190),
  error: ansis.bold.fg(196),
  fatal: ansis.bold.underline.bg(196).fg(255),
};
const logSymbols = {
  trace: '🔍',
  debug: '🐞',
  info: '💡',
  success: '✅',
  warn: '🚧',
  error: '❌',
  fatal: '💀',
};
const prettifyTime: PinoPretty.Prettifier = (inputData) => {
  const dateTime = typeof inputData === 'string' ? inputData : '';
  const luxDateTime = DateTime.fromMillis(Number(dateTime));
  const luxDate = luxDateTime.toFormat('dd-MM-yyyy');
  const luxTime = luxDateTime.toFormat('HH:mm:ss a');

  return `📆 ${ansis.gray(luxDate)} | 🕥 ${ansis.white(luxTime)}`;
};

const prettifyLevel: PinoPretty.Prettifier = (inputData) => {
  const level = typeof inputData === 'string' ? inputData : '';
  return `${logSymbols[level]} ${logSymTheme[level](level.toUpperCase())}`;
};

const pinoPrettyOptions: PrettyOptions = {
  //           //       levelFirst: true,
  messageFormat: (log, messageKey) => {
    const dateTime = prettifyTime(`${log.time}`).split('|');

    const levelHeading = `📶 ${ansis.inverse(
      `${logSymTheme[`${log.level}`]('LEVEL')}`,
    )}`;
    const date = dateTime[0] as string;
    const contextName = ansis.red(`[${log.context}]` as string);
    const pid = ansis.fg(98)(`🪪 ${ansis.gray('PID:')} (${log.pid})` as string);
    const level = prettifyLevel(`${log.level}`);
    const time = dateTime[1] as string;
    const msg = `${ansis.bold.fg(27)(`${log[messageKey]}`)}` as string;

    return msg && contextName
      ? '\n' +
          `${levelHeading}  |  ${date}  |  💻 ${contextName}  |  ${pid}` +
          '\n' +
          `${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}` +
          '\n' +
          `${level}  |  ${time}  |  🔊 ${msg}` +
          '\n\n' +
          `${ansis.fg(242)(`${'='.padStart(80, '=')}`)}`
      : '\n' +
          `${levelHeading}  |  ${date}  |  💻 ${contextName}  |  ${pid}` +
          '\n' +
          `${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}` +
          '\n' +
          `${level}  |  ${time}  |  🔊 ${msg}` +
          '\n\n' +
          `${ansis.fg(242)(`${'='.padStart(80, '=')}`)}`;
  },
  customPrettifiers: {
    time: prettifyTime,
    level: prettifyLevel,
  },
  crlf: true,
  colorize: true,
  translateTime: 'SYS:mmm dd, yyyy hh:MM:ss TT Z',
  levelFirst: true,
  ignore: 'time,pid,context,hostname,req,res,err,level',
};

export const pinoLoggerModuleOptions: Params = {
  pinoHttp: {
    autoLogging: true,
    quietReqLogger: true,
    formatters: {
      level: (label: string) => {
        return { level: label };
      },
    },
    customSuccessMessage: (req, res) => {
      return `
      REQUEST\n
        🪪 REQ-ID: ${ansis.green(`${req.id}`)}\n
        📡 METHOD: ${ansis.red(`${req.method}`)}\n
        🔗 URL: ${ansis.blue(`${req.url}`)}\n
        🏠 HOST: ${ansis.yellow(`${req.headers.host}`)}\n
        =============================\n
      RESPONSE\n
        📦 STATUS: ${ansis.white(`${res.statusCode}`)}\n
        🕥 RESPONSE TIME: ${ansis.gray(`${DateTime.fromMillis(Number(res[startTime])).toFormat('hh:mm:ss a')}`)}\n
        =============================\n
      `;
    },
    customErrorMessage(req, res, error) {
      return `
      REQUEST\n
        🪪 ID: ${ansis.green(`${req.id}`)}\n
        📡 METHOD: ${ansis.red(`${req.method}`)}\n
        🔗 URL: ${ansis.blue(`${req.url}`)}\n
        🏠 HOST: ${ansis.yellow(`${req.headers.host}`)}\n
        =============================\n
      ERROR\n
        📦 STATUS: ${ansis.bold.red(`${res.statusCode}`)}\n
        📦 MESSAGE: ${ansis.underline.red(`${error.message}`)}\n
        ==========================================================\n
        🥞 STACKTRACE:\n
        ${error.stack
          .split('\n')
          .map((line) => ansis.bold.red(line))
          .join('\n')}\n
        ===========================================================\n
        🕥 RESPONSE TIME: ${ansis.gray(`${DateTime.fromMillis(Number(res[startTime])).toFormat('hh:mm:ss a')}`)}\n
        ===========================================================\n
      `;
    },
    serializers: {
      req: (req) => {
        return {
          id: req.id,
          method: req.method,
          url: req.url,
          host: req.headers.host,
        };
      },
      res: (res) => {
        return {
          res,
        };
      },
      err: (err) => {
        return {
          id: err.id,
          message: err.message,
          stack: err.stack,
        };
      },
    },
    stream:
      process.env.NODE_ENV !== 'production'
        ? PinoPretty(pinoPrettyOptions)
        : undefined,

    mixin(mergeObject: any) {
      if (!mergeObject.msg && mergeObject.message) {
        mergeObject = { ...mergeObject, msg: mergeObject.message };
      }
      return mergeObject;
    },
    genReqId(req, res) {
      const existingID = req.id ?? req.headers['x-request-id'];
      if (existingID) {
        return existingID;
      }
      const id = randomUUID();
      res.setHeader('X-Request-Id', id);
      return id;
    },
  },
};
