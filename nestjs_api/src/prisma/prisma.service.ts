import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaClient } from '@prisma/client';
import { PinoLogger, InjectPinoLogger } from 'nestjs-pino';

@Injectable()
export class PrismaService
  extends PrismaClient
  implements OnModuleInit, OnModuleDestroy
{
  constructor(
    private configService: ConfigService,
    @InjectPinoLogger(PrismaService.name)
    private readonly logger: PinoLogger,
  ) {
    super({
      datasources: {
        db: {
          url: configService.get<string>('DATABASE_URL'),
        },
      },
    });
    this.logger.info(
      `Database URL: ${configService.get<string>('DATABASE_URL')}`,
    );
  }
  async onModuleInit() {
    const databaseUrl = this.configService.get<string>('DATABASE_URL');

    if (!databaseUrl) {
      throw new Error('DATABASE_URL is not defined');
    }

    try {
      await this.$connect();
      this.logger.info('Connected to DB');
    } catch (error) {
      this.logger.error('Failed to connect to DB', error);
      throw error;
    }
  }
  async onModuleDestroy() {
    await this.$disconnect();
    this.logger.info('Disconnected from DB');
  }
}
