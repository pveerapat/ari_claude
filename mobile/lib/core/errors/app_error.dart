/// Typed error hierarchy for ARI mobile.
/// Never expose stack traces, JWT internals, or MinIO credentials to the user.
sealed class AppError implements Exception {
  const AppError(this.message);
  final String message;

  @override
  String toString() => message;
}

class NoInternetError extends AppError {
  const NoInternetError()
      : super('No internet connection. Please check your network.');
}

class UnauthorizedError extends AppError {
  const UnauthorizedError([String? msg])
      : super(msg ?? 'Session expired. Please log in again.');
}

class ForbiddenError extends AppError {
  const ForbiddenError([String? msg])
      : super(msg ?? 'You do not have permission to perform this action.');
}

class NotFoundError extends AppError {
  const NotFoundError([String? msg])
      : super(msg ?? 'The requested resource was not found.');
}

class ValidationError extends AppError {
  final Map<String, dynamic>? detail;
  const ValidationError(String message, {this.detail}) : super(message);
}

class ServerError extends AppError {
  final int? statusCode;
  const ServerError(String message, {this.statusCode}) : super(message);
}

class TimeoutError extends AppError {
  const TimeoutError() : super('Request timed out. Please try again.');
}

class LocalStorageError extends AppError {
  const LocalStorageError(String message) : super(message);
}

class UploadError extends AppError {
  const UploadError(String message) : super(message);
}

class SyncError extends AppError {
  const SyncError(String message) : super(message);
}

class PermissionError extends AppError {
  const PermissionError(String message) : super(message);
}
