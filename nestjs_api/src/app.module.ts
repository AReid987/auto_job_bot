import { Module, OnApplicationBootstrap } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { LoggerModule } from 'nestjs-pino';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseInitModule } from './database-init/database-init.module';
import { DatabaseInitService } from './database-init/database-init.service'; // Import the service
import { HealthModule } from './health/health.module';
import { PrismaModule } from './prisma/prisma.module';

@Module({
  imports: [
    LoggerModule.forRoot({
      pinoHttp: {
        level: 'trace', // Set level to 'trace'
        customProps: () => ({
          prettyPrint: true,
          context: 'HTTP',
        }),
        transport: {
          target: 'pino-pretty',
          options: {
            singleLine: true,
            colorize: true,
            translateTime: 'SYS:mm/dd/yyyy, h:MM:ss TT Z',
            messageFormat:
              '{level} - {context} - {msg} - {if url}{url: {url}{end}',
          },
        },
      },
    }),
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '../.env',
      expandVariables: true,
    }),
    DatabaseInitModule,
    PrismaModule,
    HealthModule,
  ],
  controllers: [AppController],
  providers: [AppService], // Add the service to providers
})
export class AppModule implements OnApplicationBootstrap {
  constructor(private databaseInitService: DatabaseInitService) {}

  async onApplicationBootstrap() {
    if (!this.databaseInitService.initializeConnection()) {
      throw new Error('Failed to initialize database connection');
    }
  }
}
