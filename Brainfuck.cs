namespace BrainFuck;

public class BrainFuck
{
    private const int memoryCellCount = 256;
    private readonly char[] _memoryCells = new char[memoryCellCount];
    private int _pointer;
    private int _instructionPointer;
    private string _expression = "";

    public void Evaluate(string expr)
    {
        _expression = expr;
        while (_instructionPointer < _expression.Length)
        {
            EvaluateChar(_expression[_instructionPointer]);
        }
    }

    private void EvaluateChar(char instruction)
    {
        switch (instruction)
        {
            case '>':
                MovePointer(1);
                _instructionPointer++;
                break;
            case '<':
                MovePointer(-1);
                _instructionPointer++;
                break;
            case '+':
                _memoryCells[_pointer]++;
                _instructionPointer++;
                break;
            case '-':
                _memoryCells[_pointer]--;
                _instructionPointer++;
                break;
            case '.':
                Console.WriteLine((int)_memoryCells[_pointer]);
                _instructionPointer++;
                break;
            case ',':
                ReadInput();
                _instructionPointer++;
                break;
            case '[':
                ProcessLoopStart();
                break;
            case ']':
                ProcessLoopEnd();
                break;
            default:
                _instructionPointer++;
                break;
        }
    }

    private void MovePointer(int delta)
    {
        _pointer = (_pointer + delta) % memoryCellCount;
    }

    private void ReadInput()
    {
        int res;
        Console.WriteLine("Type a number from 0 to 255.");
        while (!int.TryParse(Console.ReadLine(), out res))
        {
            Console.WriteLine("Invalid input, must be a number between 0 and 255.");
            Console.WriteLine("Type a number from 0 to 255.");
        }

        _memoryCells[_pointer] = (char)res;
    }

    private void ProcessLoopStart()
    {
        if (_memoryCells[_pointer] != 0)
        {
            _instructionPointer++;
            return;
        }

        while (_expression[_instructionPointer] != ']')
        {
            _instructionPointer++;
        }

        _instructionPointer++;
    }
    
    private void ProcessLoopEnd()
    {
        if (_memoryCells[_pointer] == 0)
        {
            _instructionPointer++;
            return;
        }

        while (_expression[_instructionPointer] != ']')
        {
            _instructionPointer--;
        }
    }
}
