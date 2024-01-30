import { ConfigModule } from './config/config.module';
import { LoggerModule } from 'nestjs-pretty-logger';
import { Module } from '@nestjs/common';
import { DevtoolsModule } from '@nestjs/devtools-integration';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { NestLoggerService } from './logger/logger.service';

@Module({
  imports: [
    DevtoolsModule.register({
      http: process.env['NODE_ENV'] !== 'production',
    }),
    LoggerModule,
    ConfigModule,
  ],
  controllers: [AppController],
  providers: [AppService, NestLoggerService],
})
export class AppModule {}
