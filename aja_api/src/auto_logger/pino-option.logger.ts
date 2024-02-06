import ansis from 'ansis';
import { randomUUID } from 'crypto';
import { DateTime } from 'luxon';
import type { Params } from 'nestjs-pino';
import { startTime } from 'pino-http';
import type { PrettyOptions } from 'pino-pretty';
import PinoPretty from 'pino-pretty';

// let term = createTerminal();

// const termTable = (content) => {
//   const table = term.table(
//     [
//       [
//         content.row1Heading,
//         content.row2Heading,
//         content.row3Heading,
//         content.row4Heading,
//       ],
//       [
//         content.row1Content,
//         content.row2Content,
//         content.row3Content,
//         content.row4Content,
//       ],
//     ],
//     {
//       hasBorder: true,
//       contentHasMarkup: false,
//       // borderChars: 'lightRounded',
//       // borderAttr: { bgColor: 'blue' },
//       // textAttr: { bgColor: 'default' },
//       fit: true,
//     },
//   );
//   return table;
// };
// let progressBar = term.progressBar({
//   percent: true,
//   title: 'Starting',
//   eta: true,
//   inline: true,
// });
// let progress = 0;

// export const doProgress = () => {
//   progress += Math.random() / 20;
//   progressBar.update(progress);

//   if (progress > 1) {
//     setTimeout(() => {
//       term('\n');
//       process.exit();
//     }, 200);
//   } else {
//     setTimeout(doProgress, 100 + Math.random() * 400);
//   }
// };
const logSymTheme = {
  debug: ansis.bold.cyan,
  error: ansis.bold.fg(196),
  fatal: ansis.bold.underline.bg(196).fg(255),
  info: ansis.bold.fg(40),
  success: ansis.bold.fg(21),
  trace: ansis.bold.gray,
  warn: ansis.bold.fg(190),
};
const logSymbols = {
  debug: '🐞',
  error: '❌',
  fatal: '💀',
  info: '💡',
  success: '✅',
  trace: '🔍',
  warn: '🚧',
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
  colorize: true,
  crlf: true,
  customPrettifiers: {
    level: prettifyLevel,
    time: prettifyTime,
  },
  ignore: 'time,pid,reqId,responseTime,hostname,req,res,err,level',
  levelFirst: true,
  //           //       levelFirst: true,
  messageFormat: (log, messageKey) => {
    const dateTime = prettifyTime(`${log.time}`).split('|');

    const levelHeading = `📶 ${ansis.inverse(`${logSymTheme[`${log.level}`]('LEVEL')}`)}`;
    const date = dateTime[0] as string;
    const contextName = ansis.red(`💻 [${log.context}]` as string);
    const pid = ansis.fg(98)(`🪪 ${ansis.gray('PID:')} (${log.pid})` as string);
    const level = prettifyLevel(`${log.level}`);
    const time = dateTime[1] as string;
    const msg = ansis.bold.fg(27)(`🔊 ${log[messageKey]}`) as string;
    const duration = ansis.bold.fg(242)(`⏰  ${log.duration}ms` as string);
    // const tableContent = {
    //   row1Heading: levelHeading,
    //   row1Content: level,
    //   row2Heading: date,
    //   row2Content: time,
    //   row3Heading: contextName,
    //   row3Content: pid,
    //   row4Heading: msg,
    //   row4Content: duration,
    // };

    // return '';
    // return msg && contextName
    //   ? '\n' + termTable(tableContent)
    //   : '\n' + termTable(tableContent);

    return msg && contextName
      ? '\n' +
          `${levelHeading}  |  ${date}  |  ${contextName}  |  ${pid}` +
          '\n' +
          `${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}` +
          '\n' +
          `${level}   | ${time}  |  ${msg}  |  ${duration}` +
          '\n\n' +
          `${ansis.fg(242)(`${'='.padStart(80, '=')}`)}`
      : '\n' +
          `${levelHeading}  |  ${date}  |  ${contextName}  |  ${pid}` +
          '\n' +
          `${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}` +
          '\n' +
          `${level}  |  ${time}  |  ${msg}  |  ${duration}` +
          '\n\n' +
          `${ansis.fg(242)(`${'='.padStart(80, '=')}`)}`;
  },
  translateTime: 'SYS:mmm dd, yyyy hh:MM:ss TT Z',
};

export const pinoLoggerModuleOptions: Params = {
  pinoHttp: {
    autoLogging: true,
    customErrorMessage(req, res, error) {
      return `\n
        REQUEST\n
          🪪 ID: ${ansis.green(`${req.id}`)}\n
          📡 METHOD: ${ansis.red(`${req.method}`)}\n
          🔗 URL: ${ansis.blue(`${req.url}`)}\n
          🏠 HOST: ${ansis.yellow(`${req.headers.host}`)}\n
        ${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}\n
        ERROR\n
          📦 STATUS: ${ansis.bold.red(`${res.statusCode}`)}\n
          💬 MESSAGE: ${ansis.underline.red(`${error.message}`)}\n
          ${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}
        🥞 STACKTRACE:\n
          ${
            error.stack
              ? error.stack
                  .split('\n')
                  .map((line) => ansis.bold.red(line))
                  .join('\n')
              : 'Stack trace not available.'
          }\n
        ${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}\n
        🕥 RESPONSE TIME: ${ansis.gray(`+${DateTime.fromMillis(Number(res[startTime])).toFormat('S')}ms`)}
          `;
    },
    customSuccessMessage: (req, res) => {
      return `\n
        REQUEST\n
          🪪 REQ-ID: ${ansis.green(`${req.id}`)}\n
          📡 METHOD: ${ansis.red(`${req.method}`)}\n
          🔗 URL: ${ansis.blue(`${req.url}`)}\n
          🏠 HOST: ${ansis.yellow(`${req.headers.host}`)}\n
          ${ansis.fg(242).dim(`${'-'.padStart(80, '-')}`)}\n
        RESPONSE\n
          📦 STATUS: ${ansis.white(`${res.statusCode}`)}\n
          💬 MESSAGE: ${ansis.grey(`${res.statusMessage}`)}\n
          🕥 RESPONSE TIME: ${ansis.gray(`+${DateTime.fromMillis(Number(`${res[startTime]}`)).toFormat('S')}ms`)}
      `;
    },
    formatters: {
      level: (label: string) => {
        return { level: label };
      },
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
    mixin(mergeObject: any) {
      let newMergeObject = mergeObject;
      if (!newMergeObject.msg && newMergeObject.message) {
        newMergeObject = {
          ...newMergeObject,
          context: newMergeObject.context ?? 'HTTP',
          msg: newMergeObject.message,
        };
        if (newMergeObject.msg && !newMergeObject.message) {
          newMergeObject = {
            ...newMergeObject,
            context: newMergeObject.context ?? 'HTTP',
            msg: newMergeObject.msg,
          };
        }
      }
      return newMergeObject;
    },
    quietReqLogger: true,

    serializers: {
      err: (err) => {
        return {
          id: err.id,
          message: err.message,
          stack: err.stack,
        };
      },
      req: (req) => {
        return {
          host: req.headers.host,
          id: req.id,
          method: req.method,
          url: req.url,
        };
      },
      res: (res) => {
        return {
          res,
        };
      },
    },
    stream:
      process.env.NODE_ENV !== 'production'
        ? PinoPretty(pinoPrettyOptions)
        : undefined,
  },
};
