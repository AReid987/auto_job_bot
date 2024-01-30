import { NestFactory, PartialGraphHost } from '@nestjs/core';
import { FlubErrorHandler } from 'nestjs-flub';
import { AppModule } from './app.module';
import { writeFileSync } from 'fs';
import { ConfigService } from './config/config.service';
import { NestLoggerService } from './logger/logger.service';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    bufferLogs: true,
    snapshot: true,
    abortOnError: false,
  });

  const nestConfigService = app.get(ConfigService);
  const port = nestConfigService.get('PORT');

  const logger = app.get(NestLoggerService);
  app.useLogger(logger);
  app.useGlobalFilters(new FlubErrorHandler({ theme: 'dark', quote: true }));
  await app.listen(port);
  logger.log('App is running on port: ' + port);
}
bootstrap().catch(() => {
  writeFileSync('graph.json', PartialGraphHost.toString() ?? '');
  process.exit(1);
});
