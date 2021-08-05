using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace Susus_generátorus
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("Susus generátorus\nZadejte slovo a susněte ho :lenny face:");

            while (true)
            {
                Console.WriteLine("\nZadejte slovo");
                Generatorus(Console.ReadLine());
            }
        }

        private static void Generatorus(string slovo)
        {
            var samohlasky = "aeiouáéěíóúůý";
            var abeceda = "abcdefghijklmnopqrstuvwxyzáéěíóúůý";

            if (slovo.Length <= 2 || string.IsNullOrEmpty(slovo))
                return;

            slovo = Regex.Replace(slovo, @"\s+", "");

            foreach (var word in slovo)
            {
                if (!abeceda.Contains(char.ToLower(word)))
                    return;
            }

            if (samohlasky.Contains(slovo.Last()))
                slovo = slovo.Remove(slovo.Length - 1);

            Console.WriteLine(slovo + "us");
        }
    }
}