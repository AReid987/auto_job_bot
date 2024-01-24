import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { Logger, LoggerErrorInterceptor } from 'nestjs-pino';
async function bootstrap() {
  const app = await NestFactory.create(AppModule, { bufferLogs: true });
  const configService = app.get(ConfigService);
  const port = configService.get('PORT') || 3000;
  app.useLogger(app.get(Logger));
  app.useGlobalInterceptors(new LoggerErrorInterceptor());
  await app.listen(port);
  // Log with nest pino logger
  const logger = app.get(Logger);
  logger.log(`API is listening on: ${await app.getUrl()}`);
  // console.log(`API is listening on: ${await app.getUrl()}`);
}
bootstrap();
