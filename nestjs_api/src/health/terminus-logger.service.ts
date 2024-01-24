import { Injectable } from '@nestjs/common';
import { PinoLogger, InjectPinoLogger } from 'nestjs-pino';

@Injectable()
export class TerminusLoggerService {
  constructor(
    @InjectPinoLogger(TerminusLoggerService.name)
    private readonly logger: PinoLogger,
  ) {}

  log(message: any, context?: string) {
    this.logger.info(message, context);
  }

  error(message: any, trace?: string, context?: string) {
    this.logger.error(message, trace, context);
  }

  warn(message: any, context?: string) {
    this.logger.warn(message, context);
  }

  debug(message: any, context?: string) {
    this.logger.debug(message, context);
  }

  verbose(message: any, context?: string) {
    this.logger.trace(message, context);
  }
}
