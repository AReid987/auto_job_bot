// messageFormat.js
import pinoPretty from 'pino-pretty';

export default (opts) =>
  pinoPretty({
    ...opts,
    messageFormat: (log, messageKey, levelLabel) => {
      if (log.req) {
        return `${levelLabel}: ${log.timestamp} Request: id=${
          log.req.id
        }, method=${log.req.method}, url=${log.req.url}, query=${JSON.stringify(
          log.req.query,
        )}, params=${JSON.stringify(log.req.params)}, responseTime=${
          log.req.responseTime
        }`;
      }
      if (log.res) {
        return `${levelLabel}: ${log.timestamp} Response: statusCode=${log.res.statusCode}, context=${log.res.context}`;
      }
      return `${levelLabel}: ${log.timestamp} ${log[messageKey]}`;
    },
  });
