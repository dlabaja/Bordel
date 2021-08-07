using System;
using System.Collections.Generic;
using System.Threading;

namespace Tic_Tac_Toe
{
    internal class Program
    {
        private static string player1;
        private static string player2;
        private static uint pole;
        private static int curPlayer;
        private static string hra;
        private static uint spojit;

        private static Dictionary<uint, string> pozice = new Dictionary<uint, string>();

        private static void Main(string[] args)
        {
            Console.WriteLine("Vítej v piškvorkách! Nejdřív zadej své jméno"); //kolečka
            player1 = NameValidator();
            Console.WriteLine("Nyní ať si jméno vybere tvůj spoluhráč"); //křížky
            player2 = NameValidator();
            Console.WriteLine("Ještě zadej velikost hracího pole");
            PoleValidator();
            Console.WriteLine("Kolik koleček/křížků se má spojit aby dotyčný vyhrál?");
            SpojitValidator();

            Game();
        }

        private static void Game()
        {
            Console.WriteLine("Generuji nové pole...\n");
            NewGrid();
            Thread.Sleep(1000);
            Console.Clear();
            Console.WriteLine(hra);
            while (true)
            {
                if (pozice.Count == 9)
                    break;

                Console.WriteLine("\nNa tahu je hráč " + GetPlayer() + "(" + GetSymbol() + ")");

                var selectedPole = GetPole();
                while (!pozice.TryAdd(selectedPole, GetSymbol()))
                    Console.WriteLine("Tohle pole už je obsazené! Zkus to znovu");

                ReconstructGrid(selectedPole);
                Console.Clear();
                Console.WriteLine(hra);
                PiškvorkyEngine();

                curPlayer++;
            }
            FinishedGame(true);
        }

        private static void PiškvorkyEngine()
        {
            GetHorizontal("o");
            GetHorizontal("x");

            GetVertical("o");
            GetVertical("x");

            GetDiagonalLeft("o");
            GetDiagonalLeft("x");

            GetDiagonalRight("o");
            GetDiagonalRight("x");
        }

        private static void GetHorizontal(string symbol)
        {
            int souvislost = 0;
            for (uint i = 1; i < pole * pole; i++)
            {
                if (pozice.ContainsKey(i) && pozice.GetValueOrDefault(i) == symbol)
                {
                    souvislost++;
                    if (souvislost == spojit)
                        FinishedGame(false);

                    continue;
                }
                souvislost = 0;
            }
        }

        private static void GetVertical(string symbol)
        {
            foreach (var item in pozice.Keys)
            {
                if (pozice.GetValueOrDefault(item) != symbol)
                    continue;

                int souvislost = 0;
                for (uint i = 1; i <= pole; i++)
                {
                    var u = item + (i * pole);
                    if (pozice.ContainsKey(u) && pozice.GetValueOrDefault(u) == symbol)
                    {
                        Console.WriteLine("souvislost:" + souvislost);
                        souvislost++;

                        if (souvislost == spojit - 1)
                            FinishedGame(false);

                        continue;
                    }
                    souvislost = 0;
                    break;
                }
            }
        }

        private static void GetDiagonalLeft(string symbol)
        {
            foreach (var item in pozice.Keys)
            {
                if (pozice.GetValueOrDefault(item) != symbol)
                    continue;

                int souvislost = 0;
                for (uint i = 1; i <= pole; i++)
                {
                    var u = item + (i * (pole - 1));
                    if (pozice.ContainsKey(u) && pozice.GetValueOrDefault(u) == symbol)
                    {
                        Console.WriteLine("souvislost:" + souvislost);
                        souvislost++;

                        if (souvislost == spojit - 1)
                            FinishedGame(false);

                        continue;
                    }
                    souvislost = 0;
                    break;
                }
            }
        }

        private static void GetDiagonalRight(string symbol)
        {
            foreach (var item in pozice.Keys)
            {
                if (pozice.GetValueOrDefault(item) != symbol)
                    continue;

                int souvislost = 0;
                for (uint i = 1; i <= pole; i++)
                {
                    var u = item + (i * (pole + 1));
                    if (pozice.ContainsKey(u) && pozice.GetValueOrDefault(u) == symbol)
                    {
                        souvislost++;

                        if (souvislost == spojit - 1)
                            FinishedGame(false);

                        continue;
                    }
                    souvislost = 0;
                    break;
                }
            }
        }

        private static void FinishedGame(bool isDraw)
        {
            Console.ForegroundColor = ConsoleColor.Green;
            if (isDraw)
                Console.WriteLine("Remíza!");
            else
                Console.WriteLine("Vyhrál " + GetPlayer()); //...
            pozice.Clear();
            hra = "";
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("Zmáčkněte jakoukoliv klávesu pro nové kolo");
            Console.ReadKey();
            Console.Clear();
            Game();
        }

        private static void ReconstructGrid(uint selPole)
        {
            hra = hra.Replace("|" + selPole.ToString("D2") + "|", "| " + GetSymbol() + "|");
        }

        private static string GetPlayer()
        {
            if (curPlayer >= 2)
                curPlayer = 0;
            if (curPlayer == 0)
                return player1;
            return player2;
        }

        private static string GetSymbol()
        {
            if (curPlayer >= 2)
                curPlayer = 0;
            if (curPlayer == 0)
                return "o";
            return "x";
        }

        private static uint GetPole()
        {
            uint i;
            while (!uint.TryParse(Console.ReadLine(), out i) || i > pole * pole)
                Console.WriteLine("Neplatné číslo");
            return i;
        }

        private static void NewGrid()
        {
            for (int i = 1; i <= pole * pole; i++)
            {
                if (i % pole == 0)
                {
                    hra += "|" + i.ToString("D2") + "|\n";
                    continue;
                }
                hra += "|" + i.ToString("D2");
            }
        }

        private static string NameValidator()
        {
            var name = Console.ReadLine();
            while (string.IsNullOrWhiteSpace(name))
            {
                Console.WriteLine("Neplatné jméno!");
                name = Console.ReadLine();
            }
            return name;
        }

        private static void PoleValidator()
        {
            while (!uint.TryParse(Console.ReadLine(), out pole))
                Console.WriteLine("Neplatné číslo");
            if (pole > 10 || pole < 3)
            {
                Console.WriteLine("Maximální velikost pole překročena, nastavuji 10");
                pole = 10;
            }
        }

        private static void SpojitValidator()
        {
            while (!uint.TryParse(Console.ReadLine(), out spojit))
                Console.WriteLine("Neplatné číslo");
            if (spojit > pole || spojit < 3)
            {
                Console.WriteLine("Maximální velikost překročena, nastavuji " + pole);
                spojit = pole;
            }
        }
    }
}