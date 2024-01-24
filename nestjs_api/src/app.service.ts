import { Injectable, OnModuleInit } from '@nestjs/common';
import { DatabaseInitService } from './database-init/database-init.service';
@Injectable()
export class AppService implements OnModuleInit {
  constructor(private readonly databaseInitService: DatabaseInitService) {}
  async onModuleInit() {
    // await this.databaseInitService.onModuleInit();
  }
  getHello(): string {
    return 'Hello World!';
  }
}
