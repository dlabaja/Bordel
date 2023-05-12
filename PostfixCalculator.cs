using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PostfixCalculator
{
	public class PostfixCalculator
	{
		Stack<double> buffer = new Stack<double>();
		Dictionary<string, Func<double>> operations;

		public void InitDict() => operations = new Dictionary<string, Func<double>>()
		{
			{ "+", () => buffer.Pop() + buffer.Pop()},
			{ "-", () => buffer.Pop() - buffer.Pop()},
			{ "*", () => buffer.Pop() * buffer.Pop()},
			{ "/", () => {
				var num1 = buffer.Pop();
				var num2 = buffer.Pop();
				if (num2 == 0) throw new Exception("Math error");
				return num1 / num2; }
				},
			{ "%", () => buffer.Pop() % buffer.Pop()},
			{ "sin", () => Math.Sin(buffer.Pop())},
			{ "cos", () => Math.Cos(buffer.Pop())},
			{ "tg", () => Math.Sin(buffer.Pop())},
			{ "cotg", () => {
				var num1 = buffer.Pop();
				var num2 = buffer.Pop();
				if (num2 == 0) throw new Exception("Math error");
				return Math.Cos(num1) / Math.Sin(num2); } },
			{ "pow", () => Math.Pow(buffer.Pop(), 2)},
			{ "sqrt", () =>{
				var num = buffer.Pop();
				if (num < 0) throw new Exception("Math error");
				return Math.Sqrt(num); } },
			{ "log", () => {
				var num = buffer.Pop();
				if (num <= 0) throw new Exception("Math error");
				return Math.Log10(num); }},
			{ "ln", () => {
				var num = buffer.Pop();
				if (num <= 0) throw new Exception("Math error");
				return Math.Log(num); }},
			{ "abs", () => Math.Abs(buffer.Pop())},
			{ "π", () => Math.PI},
			{ "e", () => Math.E}
		};

		public object Calculate(dynamic[] commands)
		{
			try
			{
				InitDict();
				for (int i = 0; i < commands.Length; i++)
				{
					if (operations.ContainsKey(Convert.ToString(commands[i])))
						buffer.Push(operations[Convert.ToString(commands[i])]());
					else
						buffer.Push(Convert.ToDouble(commands[i]));
				}
				if (buffer.Count > 1)
					throw new Exception("Invalid Syntax");
			}
			catch (Exception e)
			{
				return e.Message;
			}
			return buffer.Pop();
		}

		public dynamic[] InfixToPostfix(string infix)
		{
			InitDict();
			var postfix = new List<dynamic>();
			var stack = new Stack<string>();

			infix += " )";
			

			foreach (var item in infix.Split())
			{
				if (item == "(")
					stack.Push("(");
				else if (double.TryParse(item, out var d))
					postfix.Add(d);
				else if (item == ")")
				{
					while (stack.Count > 0 && stack.Peek() != "(")
						postfix.Add(stack.Pop());
					if (stack.Count > 0) stack.Pop();
				}
				else
				{
					while (stack.Count > 0 && stack.Peek() != "(" && GetPrecedence(stack.Peek()) >= GetPrecedence(item))
						postfix.Add(stack.Pop());
					stack.Push(item);
				}
			}
			while (stack.Count > 0)
				postfix.Add(stack.Pop());

			return postfix.ToArray();
		}

		private static int GetPrecedence(string op)
		{
			switch (op)
			{
				case "+":
				case "-":
					return 1;
				case "*":
				case "/":
				case "%":
					return 2;
				default:
					return 0;
			}
		}
	}
}
