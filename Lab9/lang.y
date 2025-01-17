%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
extern void yyerror(const char *s);

%}

%union {
    int ival;
    float fval;
    char cval;
    char *sval;
}

%token <ival> INTEGER
%token <fval> FLOAT
%token <sval> STRING
%token <cval> CHARACTER
%token BOOL
%token <sval> IDENTIFIER
%token CONSTANT
%token TYPE PRINT IF ELSE FOR IN RETURN
%token ASSIGN OPERATOR
%token LPAREN RPAREN LBRACKET RBRACKET LBRACE RBRACE SEMICOLON COMMA

%type <sval> program statement_list statement assign_statement declaration_statement
%type <sval> expression term factor io_statement argument_list
%type <sval> control_statement loop_statement list element_list condition operator
%type <sval> function_statement type parameter_list

%%

program
    : statement_list
    ;

statement_list
    : statement SEMICOLON
    | statement SEMICOLON statement_list
    ;

statement
    : assign_statement
    | declaration_statement
    | io_statement
    | control_statement
    | loop_statement
    ;

assign_statement
    : IDENTIFIER ASSIGN expression
    ;

declaration_statement
    : TYPE IDENTIFIER
    | TYPE assign_statement
    ;

expression
    : list
    | term
    | term OPERATOR expression
    ;

term
    : factor
    | factor OPERATOR term
    ;

factor
    : IDENTIFIER
    | CONSTANT
    | LPAREN expression RPAREN
    ;

io_statement
    : PRINT LPAREN argument_list RPAREN
    ;

argument_list
    : IDENTIFIER
    | STRING
    | IDENTIFIER COMMA argument_list
    ;

control_statement
    : IF LPAREN condition RPAREN LBRACE statement_list RBRACE
    | IF LPAREN condition RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    ;

loop_statement
    : FOR LPAREN IDENTIFIER IN list RPAREN LBRACE statement_list RBRACE
    | FOR LPAREN IDENTIFIER IN IDENTIFIER RPAREN LBRACE statement_list RBRACE
    ;

list
    : LBRACKET element_list RBRACKET
    ;

element_list
    : CONSTANT
    | CONSTANT COMMA element_list
    ;

condition
    : expression operator expression
    ;

operator
    : OPERATOR
    ;

function_statement
    : type IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE
    ;

type
    : TYPE
    ;

parameter_list
    : IDENTIFIER
    | IDENTIFIER COMMA parameter_list
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    printf("Enter your program: \n");
    yyparse();
    return 0;
}