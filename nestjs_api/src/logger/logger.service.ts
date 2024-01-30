import { ConsoleLoggerOptions, Injectable } from '@nestjs/common';
import { Logger } from 'nestjs-pretty-logger';
import chalk from 'chalk';

@Injectable()
export class NestLoggerService extends Logger {
  private chalkInstance = chalk;

  constructor(context: string, options: ConsoleLoggerOptions) {
    super(context, options);
  }

  log(message: any, context?: string) {
    super.log(this.chalkInstance.greenBright(message), context);
  }
}
