import { Module } from '@nestjs/common';
import { PrismaModule } from 'src/prisma/prisma.module';
import { HealthController } from './heath.controller';
import { TerminusLoggerService } from './terminus-logger.service';
import { TerminusModule } from '@nestjs/terminus';
@Module({
  imports: [
    TerminusModule.forRoot({
      logger: TerminusLoggerService,
      errorLogStyle: 'pretty',
    }),
    PrismaModule,
  ],
  controllers: [HealthController],
})
export class HealthModule {}
