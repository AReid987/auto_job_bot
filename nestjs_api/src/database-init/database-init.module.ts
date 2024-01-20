import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { DatabaseInitService } from './database-init.service';
@Module({
  imports: [ConfigModule],
  providers: [DatabaseInitService],
})
export class DatabaseInitModule {}
