/* The AppModule class is a module in a NestJS application that imports the DevtoolsModule and
registers the AppController and AppService. */
import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DevtoolsModule } from '@nestjs/devtools-integration';
import { AutoLoggerModule } from './auto_logger/auto_logger.module';

// *ANCHOR - The @Module() decorator is used to define a module and its configuration.
@Module({
  /* The imports array is used to import other modules that this module depends on. */
  imports: [
    DevtoolsModule.register({
      // Registering the DevtoolsModule
      http: process.env.NODE_ENV !== 'production',
    }),
    AutoLoggerModule,
  ],
  /* The controllers array is used to specify the controllers that belong to this module. */
  controllers: [AppController],
  /* The providers array is used to specify the services that belong to this module. */
  providers: [AppService],
})
/* The AppModule class is exported so that it can be used by other modules. */
export class AppModule {}
