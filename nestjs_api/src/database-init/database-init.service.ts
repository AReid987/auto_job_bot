import { Injectable, Logger } from '@nestjs/common';
import { Client } from 'pg';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class DatabaseInitService {
  private dbClient: Client;
  private readonly logger = new Logger(DatabaseInitService.name);
  private isConnected: boolean = false;
  constructor(private configService: ConfigService) {
    this.dbClient = new Client({
      host: this.configService.get<string>('POSTGRES_HOST'),
      port: parseInt(this.configService.get<string>('POSTGRES_PORT') || '5432'),
      user: this.configService.get<string>('POSTGRES_USER'),
      password: this.configService.get<string>('POSTGRES_PASSWORD'),
      database: 'postgres', // Connect to the default 'postgres' database
    });

    this.logger.log('DatabaseInitService constructed');
  }

  async initializeConnection(): Promise<void> {
    this.logger.log('initializeConnection called');
    await this.waitForDb();
    //   await this.ensureDatabase();
    this.isConnected = true;
  }

  isDatabaseConnected(): boolean {
    return this.isConnected;
  }
  private async waitForDb(retries = 5, delay = 3000): Promise<void> {
    try {
      this.logger.log('Waiting for database...');
      // if (!this.dbClient._connected){
      //   await this.dbClient.connect();
      // }
      // await this.dbClient.connect();
      this.logger.log('Connected to the database.', this.dbClient.user);
    } catch (err) {
      if (retries > 0 && err.message.includes('ECONNREFUSED')) {
        this.logger.debug(
          `Waiting for the database... Retries left: ${retries}`,
        );
        await new Promise((resolve) => setTimeout(resolve, delay));
        return this.waitForDb(retries - 1, delay);
      }
      this.logger.error('Error connecting to the database', err);
      throw err;
    }
  }

  // private async ensureDatabase() {
  //   const dbName = this.configService.get<string>('POSTGRES_DB');
  //   const dbUser = this.configService.get<string>('POSTGRES_USER');
  //   const res = await this.dbClient.query(
  //     `SELECT 1 FROM pg_database WHERE datname='${dbName}'`,
  //   );

  //   if (res.rowCount === 0) {
  //     await this.dbClient.query(
  //       `CREATE DATABASE "${dbName}" WITH OWNER "${dbUser}"`,
  //     );
  //     this.logger.log(`Database ${dbName} created`);
  //   } else {
  //     this.logger.log(`Database ${dbName} already exists`);
  //   }
  // }
}
