// import { Module } from '@nestjs/common';
// import { AutoLoggerService } from './auto_logger.service.js';
// import { LoggerModule } from 'nestjs-pino';

// @Module({
//   providers: [AutoLoggerService],
//   exports: [AutoLoggerService],
//   imports: [
//     LoggerModule.forRoot({
//       pinoHttp: {
//         transport:
//           process.env.NODE_ENV !== 'production'
//             ? {
//                 target: 'pino-pretty',
//                 options: {
//                   colorize: true,
//                   levelFirst: true,
//                   translateTime: 'SYS:yyyy-mm-dd HH:MM:ss',
//                   singleLine: true,
//                   messageFormat: `${`[{context}]`} ${`{msg}`}`,
//                   ignore: 'hostname,context',
//                 },
//               }
//             : undefined,
//         // customProps: () => ({ context: 'HTTP' }),
//       },
//     }),
//   ],
// })
// export class AutoLoggerModule {}
