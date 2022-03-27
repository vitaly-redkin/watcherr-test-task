import React from 'react';
import { Container, Row, Col, Input, Button } from 'reactstrap';
import debounce from 'lodash/debounce';

import { StoreModel } from './StoreModel';
import { ApiResultModel } from './ApiResultModel';

import './App.css';

const PAGE_SIZE = 3; // Default page size

/**
 * Composes API end point URL for fetching stores.
 * @param q string to search the store by
 * @param startWith number of the store to return the data from
 * @param n number of stores to return
 * @returns store search API end point URL
 */
function composeFetchUrl(q: string, startWith: number, n: number): string {
  return `http://localhost:8888/task2?q=${encodeURIComponent(q)}&start_with=${startWith}&n=${n}`;
}

/**
 * Application component.
 */
function App() {
  const [query, setQuery] = React.useState<string>('');
  const [stores, setStores] = React.useState<StoreModel[]>([]);
  const [totalCount, setTotalCount] = React.useState<number>(0);

 /**
  * Debounced function to fetch stores page.
  * @param q string to search the store by
  * @param startWith number of the store to return the data from (0 starts new search)
  */
  const fetchStores = debounce(React.useCallback(
    (q: string, startWith: number) => {
      fetch(
        composeFetchUrl(q.trim(), startWith, PAGE_SIZE),
        {
          method: 'GET',
          mode: 'cors',
        })
        .then(response => response.json())
        .then((data: ApiResultModel) => {
          const newStores: StoreModel[] = (startWith === 0 ? data.portion : [...stores, ...data.portion]);
          setStores(newStores);
          setTotalCount(data.total_count);
          });
    },
    [stores]),
    100
  );

  /**
   * Query change event handler.
   * @param e change event
   */
  const onQueryChange = React.useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const q: string = e.target.value;
      setQuery(q);
      fetchStores(q, 0);
    },
    [fetchStores]
  );

  /**
   * Fetches the next page with stores by the current search query.
   */
  const showMore = React.useCallback(
    () => {
      fetchStores(query, stores.length)
    },
    [query, stores.length, fetchStores]
  );

  /**
   * Renders the component.
   */
  const render = (): JSX.Element => {
    return (
      <div className="App">
        <Container className='pt-4 w-50'>
          <Row>
            <Col className='col-12'>
              <Input type="text" value={query} onChange={onQueryChange} className="w-100"></Input>
            </Col>

          </Row>
          {totalCount > 0 ? (
            <>
              <Row className='pt-4'>
                <Col className='col-12'>
                  {stores.length} store(s) of {totalCount} shown
                </Col>
              </Row>
              {stores.map(s => (
                <Row key={s.name + s.postcode} style={{height: '50px'}}>
                  <Col className='col-8'>{s.name}</Col>
                  <Col className='col-4'>{s.postcode}</Col>
                </Row>
              ))}
              {stores.length < totalCount &&
                <Button color='primary' outline className='w-100' onClick={showMore}>
                  More
                </Button>

              }
            </>
            ) : (
            <Row>
              <Col className='col-12'>
                Please change the search criteria to find some stores
              </Col>
            </Row>
          )}
        </Container>
      </div>
    );
  }

  return render();
}

export default App;
