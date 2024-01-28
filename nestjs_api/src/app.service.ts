import { Injectable } from '@nestjs/common';
@Injectable()
export class AppService {
  // constructor(private readonly logger = new Logger(AppService.name)) {}
  getHello(): string {
    return 'Hello World!';
  }
}
