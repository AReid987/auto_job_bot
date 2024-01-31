import { Test, TestingModule } from '@nestjs/testing';
import { NestLoggerService } from './logger.service';
import { LoggerService } from '@nestjs/common';

describe('LoggerService', () => {
  let service: LoggerService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [NestLoggerService],
    }).compile();

    service = module.get<LoggerService>(NestLoggerService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
