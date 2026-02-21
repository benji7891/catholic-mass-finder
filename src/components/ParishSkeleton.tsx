/**
 * Skeleton loading component for parish cards
 * Provides better perceived performance than a spinner
 */
export default function ParishSkeleton() {
  return (
    <div className="animate-pulse rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      {/* Header with name and distance */}
      <div className="mb-3 flex items-start justify-between">
        <div className="flex-1">
          {/* Church name */}
          <div className="mb-2 h-5 w-3/4 rounded bg-gray-200"></div>
          {/* Address */}
          <div className="h-4 w-full rounded bg-gray-100"></div>
        </div>
        {/* Distance badge */}
        <div className="ml-3 h-6 w-16 rounded-full bg-gray-200"></div>
      </div>

      {/* Contact info */}
      <div className="mb-3 space-y-2">
        <div className="h-3 w-2/3 rounded bg-gray-100"></div>
        <div className="h-3 w-1/2 rounded bg-gray-100"></div>
      </div>

      {/* Schedule placeholder */}
      <div className="space-y-2 border-t border-gray-100 pt-3">
        <div className="h-3 w-full rounded bg-gray-100"></div>
        <div className="h-3 w-5/6 rounded bg-gray-100"></div>
        <div className="h-3 w-4/5 rounded bg-gray-100"></div>
      </div>

      {/* Action buttons */}
      <div className="mt-4 flex gap-2">
        <div className="h-9 flex-1 rounded-lg bg-gray-200"></div>
        <div className="h-9 flex-1 rounded-lg bg-gray-200"></div>
      </div>
    </div>
  );
}

/**
 * Container for multiple skeleton cards
 */
export function ParishSkeletonList({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, index) => (
        <ParishSkeleton key={index} />
      ))}
    </div>
  );
}
