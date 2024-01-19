import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { Logger } from 'nestjs-pino';
async function bootstrap() {
  const app = await NestFactory.create(AppModule, { bufferLogs: true });
  const configService = app.get(ConfigService);
  const port = configService.get('PORT') || 3000;
  app.useLogger(app.get(Logger));
  await app.listen(port);
  console.log(`API is listening on: ${await app.getUrl()}`);
}
bootstrap();