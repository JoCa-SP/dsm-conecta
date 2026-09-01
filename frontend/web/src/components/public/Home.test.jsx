// src/components/__tests__/Home.test.jsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import Home from '../public/Home';

describe('Home component', () => {
  it('deve renderizar o título principal', () => {
    render(<Home />);
    expect(screen.getByText(/Bem-vindo ao DSM Conecta/i)).toBeInTheDocument();
  });
});