import { ConfigService } from '@nestjs/config';
import { NestFactory, PartialGraphHost } from '@nestjs/core';
import { writeFileSync } from 'fs'; // import { Logger, LoggerErrorInterceptor } from 'nestjs-pino';import { PinoLoggerService } from './logger/pino-logger.service';
import { Logger } from 'nestjs-pino';
import { AppModule } from './app.module';
async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    bufferLogs: true,
    abortOnError: false,
    snapshot: true,
  });
  const configService = app.get(ConfigService);
  const port = configService.get('PORT') || 3000;
  const logger = app.get(Logger);
  app.useLogger(logger);
  await app.listen(port);
  logger.log(`API is listening on: ${await app.getUrl()}`);
}

bootstrap().catch(() => {
  writeFileSync('graph.json', PartialGraphHost.toString() ?? '', 'utf-8');
  process.exit(1);
});
