import { Injectable } from '@nestjs/common';
import { Logger } from '@nestjs/common';
@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);
  getHello(): string {
    return 'Hello World!';
  }

  getFavicon(): string {
    return 'favicon.ico';
  }
}
