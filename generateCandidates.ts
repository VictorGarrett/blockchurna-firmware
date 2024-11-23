const data = [
  "Aracaju",
  "Belém",
  "Belo Horizonte",
  "Boa Vista",
  "Brasília",
  "Campinas",
  "Campo Grande",
  "Cuiabá",
  "Curitiba",
  "Florianópolis",
  "Fortaleza",
  "Foz do Iguaçu",
  "Goiânia",
  "João Pessoa",
  "Londrina",
  "Macapá",
  "Maceió",
  "Manaus",
  "Natal",
  "Palmas",
  "Porto Alegre",
  "Porto Velho",
  "Recife",
  "Rio Branco",
  "Rio de Janeiro",
  "Salvador",
  "São Carlos",
  "São Luís",
  "São Paulo",
  "Teresina",
  "Vitória",
  "Votuporanga",
];

const result: any = {};

const generateRandomCandidate = (digits: number) => {
  const power = 10 ** (digits - 1);
  return Math.floor(power + Math.random() * 9 * power);
};

data.forEach((city: string) => {
  result[city] = {
    prefeito: [generateRandomCandidate(5), generateRandomCandidate(5)],
    vereador: [generateRandomCandidate(2), generateRandomCandidate(2)],
  };
});

console.log(result);
