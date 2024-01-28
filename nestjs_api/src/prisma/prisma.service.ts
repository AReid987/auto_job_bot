import {
  Injectable,
  Logger,
  OnModuleDestroy,
  OnModuleInit,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Prisma, PrismaClient } from '@prisma/client';
// import { PinoLogger, InjectPinoLogger } from 'nestjs-pino';

@Injectable()
export class PrismaService
  extends PrismaClient<Prisma.PrismaClientOptions, Prisma.LogLevel>
  implements OnModuleInit, OnModuleDestroy
{
  constructor(
    private readonly logger = new Logger(PrismaService.name),
    private configService: ConfigService,
    // @InjectPinoLogger(PrismaService.name)
    // private readonly logger: PinoLogger,
    // private databaseInitService: DatabaseInitService, // Inject DatabaseInitService
  ) {
    super({
      log: [
        { emit: 'event', level: 'query' },
        { emit: 'event', level: 'error' },
        { emit: 'event', level: 'info' },
        { emit: 'event', level: 'warn' },
      ],
      datasources: {
        db: {
          url: configService.get<string>('DATABASE_URL'),
        },
      },
    });
  }
  async onModuleInit() {
    this.logger.log(
      `Database URL: ${this.configService.get<string>('DATABASE_URL')}`,
    );

    const databaseUrl = this.configService.get<string>('DATABASE_URL');

    if (!databaseUrl) {
      throw new Error('DATABASE_URL is not defined');
    }

    // await this.$connect();
    // this.logger.log('Connected to DB');

    this.$on('info', (message) => {
      this.logger.log('Prisma log: ', message);
    });
    this.$on('warn', (message) => {
      this.logger.warn('Prisma Warning: ', message);
    });

    this.$on('query', (message) => {
      this.logger.debug('Prisma Query:');
      this.logger.debug(`Query: ${message.query}`);
      this.logger.debug(`Params: ${message.params}`);
      this.logger.debug(`Duration: ${message.duration}ms`);
    });

    this.$on('error', (message) => {
      this.logger.error('Prisma Error: ', message);
    });
  }
  async onModuleDestroy() {
    await this.$disconnect();
    this.logger.log('Disconnected from DB');
  }
}
