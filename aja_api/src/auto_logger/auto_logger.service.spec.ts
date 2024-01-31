import { Test, TestingModule } from '@nestjs/testing';
import { AutoLoggerService } from './auto_logger.service';

describe('AutoLoggerService', () => {
  let service: AutoLoggerService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AutoLoggerService],
    }).compile();

    service = module.get<AutoLoggerService>(AutoLoggerService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
