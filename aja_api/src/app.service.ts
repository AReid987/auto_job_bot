import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class AppService {
  private readonly logger = new Logger(AppService.name);

  getFavicon(): string {
    this.logger.verbose({ message: 'redirect to getHello' });
    return 'favicon.ico';
  }

  getHello(): string {
    this.logger.log({ message: 'Hello World!' });
    return 'Hello World!';
  }
}
