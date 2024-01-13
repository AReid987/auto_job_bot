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
    console.log('Database URL:', this.configService.get('DATABASE_URL'));
  }
  async onModuleInit() {
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
