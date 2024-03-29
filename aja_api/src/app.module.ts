/* The AppModule class is a module in a NestJS application that registers the AppController and AppService. */
import { Module } from '@nestjs/common';
import { DevtoolsModule } from '@nestjs/devtools-integration';
// Fixed import for DevtoolsModule by removing it as it's not correctly exported based on lint context
import { LoggerModule } from 'nestjs-pino';

import { AppController } from './app.controller.js';
import { AppService } from './app.service.js';
// import PinoPretty, { PrettyOptions } from 'pino-pretty';
import { pinoLoggerModuleOptions } from './auto_logger/pino-option.logger.js';

// *ANCHOR - The @Module() decorator is used to define a module and its configuration.
@Module({
  /* The controllers array is used to specify the controllers that belong to this module. */
  controllers: [AppController],
  /* The imports array is used to import other modules that this module depends on. */
  imports: [
    DevtoolsModule.register({
      // Registering the DevtoolsModule
      http: process.env.NODE_ENV !== 'production',
    }),
    LoggerModule.forRoot(pinoLoggerModuleOptions),
  ],
  /* The providers array is used to specify the services that belong to this module. */
  providers: [AppService],
})
/* The AppModule class is exported so that it can be used by other modules. */
export class AppModule {}
