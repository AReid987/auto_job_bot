import { Controller, Get, Redirect } from '@nestjs/common';

import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Redirect('/')
  @Get('favicon.ico')
  getFavicon() {
    return this.appService.getFavicon();
  }

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}
