import { Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { DatabaseInitModule } from 'src/database-init/database-init.module';

@Module({
  imports: [DatabaseInitModule],
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
