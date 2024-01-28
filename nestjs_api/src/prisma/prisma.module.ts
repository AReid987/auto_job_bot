import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { DatabaseInitModule } from 'src/database-init/database-init.module';
import { PrismaService } from './prisma.service';

@Module({
  imports: [ConfigModule, DatabaseInitModule],
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
