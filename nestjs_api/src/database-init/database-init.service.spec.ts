import { Test, TestingModule } from '@nestjs/testing';
import { DatabaseInitService } from './database-init.service';
import { ConfigService } from '@nestjs/config';

describe('DatabaseInitService', () => {
  let service: DatabaseInitService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ConfigService, DatabaseInitService],
    }).compile();

    service = module.get<DatabaseInitService>(DatabaseInitService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
