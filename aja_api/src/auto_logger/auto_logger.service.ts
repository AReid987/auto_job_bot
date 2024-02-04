// import { Inject, Injectable } from '@nestjs/common';
// import { PinoLogger, Params, PARAMS_PROVIDER_TOKEN } from 'nestjs-pino';

// @Injectable()
// export class AutoLoggerService extends PinoLogger {
//   constructor(@Inject(PARAMS_PROVIDER_TOKEN) params: Params) {
//     super({ pinoHttp: params.pinoHttp });
//   }

//   setContext(context: string): void {
//     this.context = context;
//   }

//   log(message: string): void {
//     const formattedMessage = `${message}`;
//     this.info(formattedMessage);
//   }
// }
