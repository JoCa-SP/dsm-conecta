import { render, screen } from '@testing-library/react';
import App from './App';

test('renderiza o título "Get started"', () => {
  render(<App />);
  const headingElement = screen.getByText(/Get started/i);
  expect(headingElement).toBeInTheDocument();
});