import { NestFactory } from '@nestjs/core';
import {
  FastifyAdapter,
  NestFastifyApplication,
} from '@nestjs/platform-fastify';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

// * SECTION -  This function initializes the Nest.js application.
// * @param {NestFactory} NestFactory - The Nest factory class.
// * ANCHOR -  @param {AppModule} AppModule - The root application module.
//  * @param {FastifyAdapter} FastifyAdapter - The Fastify adapter class.
//  * @param {object} options - The application configuration options.
//  * @param {boolean} [options.snapshot=true] - Whether to enable the Nest snapshot feature.
//  * @returns {Promise<NestFastifyApplication>} The initialized Nest application.

async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter(),
    { snapshot: true },
  );
  const options = new DocumentBuilder()
    .setTitle('Auto Job App API')
    .setDescription(
      'Your very own crew of Autonomous AI agents to help you find a job.',
    )
    .setVersion('1.0')
    .addServer('http://localhost:3000', 'Local development server')
    .addServer('https://production-url-coming.soon', 'Production server')
    .addTag('Auto Job App API')
    .build();

  const document = SwaggerModule.createDocument(app, options);
  SwaggerModule.setup('api', app, document);

  await app.listen(3000);
}
bootstrap();
