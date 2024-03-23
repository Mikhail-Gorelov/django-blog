import http from 'k6/http';

export const options = {
  scenarios: {
    api_test: {
      executor: 'ramping-vus',
      startvus: 10,
      stages: [
        {duration: '10s', target: 70},
        {duration: '20s', target: 30},
        {duration: '10s', target: 0},
      ],
      gracefulRampDown: "1s",
    }
  },
  thresholds: {
    'http_req_duration': ['p(95)<300'],
    'http_req_failed': ['rate<0.001'],
  },
};

export function getPosts() {
  http.get('http://localhost:8008/posts/');
}

export function getCategories() {
  http.get('http://localhost:8008/categories/');
}

export default function () {
  getPosts();
  getCategories();
}