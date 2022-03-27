import { StoreModel } from './StoreModel';

/**
 * Interface for the API results.
 */
export interface ApiResultModel {
  portion: StoreModel[],
  total_count: number;
}
