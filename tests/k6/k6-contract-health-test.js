import http from 'k6/http';
import { check, group } from 'k6';

export const options = {
  stages: [
    { duration: '2s', target: 1 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function () {
  group('Health Endpoint Contract Tests', () => {
    const healthResponse = http.get('http://localhost:8000/api/health');
    check(healthResponse, {
      'Status code is 200': (r) => r.status === 200,
    });

    const body = JSON.parse(healthResponse.body);
    check(body, {
      'Response has status field': (obj) => 'status' in obj,
      'Status field is "ok"': (obj) => obj.status === 'ok',
      'Response has auth field': (obj) => 'auth' in obj,
      'Auth field is string': (obj) => typeof obj.auth === 'string',
      'Auth field is enabled or disabled': (obj) => ['enabled', 'disabled'].includes(obj.auth),
      'Response has auth_type field': (obj) => 'auth_type' in obj,
      'Response has header_name field': (obj) => 'header_name' in obj,
    });

    check(healthResponse, {
      'Content-Type is application/json': (r) => r.headers['Content-Type'].includes('application/json'),
    });
  });
}