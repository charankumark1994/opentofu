resource "aws_lambda_function" "cleanup" {
  function_name = "aws-auto-cleanup"
  role          = aws_iam_role.lambda_cleanup_role.arn
  handler       = "cleanup.lambda_handler"
  runtime       = "python3.11"
  timeout       = 300

  filename         = "../lambda/cleanup.zip"
  source_code_hash = filebase64sha256("../lambda/cleanup.zip")
}
