import { Module } from '@nestjs/common';
import { LoggerModule } from 'nestjs-pino';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaModule } from './prisma/prisma.module';
import { DatabaseInitModule } from './database-init/database-init.module';
@Module({
  imports: [
    LoggerModule.forRoot({
      pinoHttp: {
        transport: {
          target: 'pino-pretty',
          options: {
            singleLine: true,
            colorize: true,
            translateTime: 'UTC:mm/dd/yyyy, h:MM:ss TT Z',
          },
        },
      },
    }),
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '../.env',
      expandVariables: true,
    }),
    PrismaModule,
    DatabaseInitModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
