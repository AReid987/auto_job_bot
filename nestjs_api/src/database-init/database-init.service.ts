import { Injectable, OnModuleInit } from '@nestjs/common';
import { Client } from 'pg';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class DatabaseInitService implements OnModuleInit {
  private dbClient: Client;

  constructor(private configService: ConfigService) {
    this.dbClient = new Client({
      host: this.configService.get<string>('POSTGRES_HOST'),
      port: parseInt(this.configService.get<string>('PORT') || '5432'),
      user: this.configService.get<string>('POSTGRES_USER'),
      password: this.configService.get<string>('POSTGRES_PASSWORD'),
      database: 'postgres',
    });
  }

  async onModuleInit() {
    await this.dbClient.connect();
    await this.ensureDatabase();
    await this.dbClient.end();
  }

  private async ensureDatabase() {
    const dbName = this.configService.get<string>('POSTGRES_DB');
    const res = await this.dbClient.query(
      `SELECT 1 FROM pg_database WHERE datname='${dbName}'`,
    );

    if (res.rowCount === 0) {
      await this.dbClient.query(`CREATE DATABASE "${dbName}"`);
      console.log(`Database ${dbName} created`);
    } else {
      console.log(`Database ${dbName} already exists`);
    }
  }
}
