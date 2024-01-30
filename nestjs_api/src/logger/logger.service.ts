import { ConsoleLoggerOptions, Injectable } from '@nestjs/common';
import { Logger } from 'nestjs-pretty-logger';
import chalk from 'chalk';

@Injectable()
export class NestLoggerService extends Logger {
  private chalkInstance;

  constructor(context: string, options: ConsoleLoggerOptions) {
    super(context, options);
    this.chalkInstance = chalk;
  }

  // log(message: any, context?: string) {
  //   super.log(this.chalkInstance.greenBright(message), context);
  // }
}
